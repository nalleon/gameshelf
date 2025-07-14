package es.gameshelf.domain.services;

import es.gameshelf.domain.Edition;
import es.gameshelf.domain.interfaces.repository.IEditionRepository;
import es.gameshelf.domain.interfaces.service.IEditionService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

/**
 * @author Nabil L. A. @nalleon
 */
@Service
public class EditionService implements IEditionService {
    /**
     * Properties
     */
    IEditionRepository repository;

    /**
     * Setter for the autowired service
     * @param repository of the service
     */
    @Autowired
    public void setRepository(IEditionRepository repository) {
        this.repository = repository;
    }

    @Override
    public Edition add(String name, String description) {
        Edition item = new Edition();
        item.setName(name);
        item.setAdditionalText(description);

        return repository.save(item);
    }

    @Override
    public List<Edition> findAll() {
        return repository.findAll();
    }

    @Override
    public Edition findById(Integer id) {
        return repository.findById(id);
    }

    @Override
    public Edition findByName(String name) {
        return repository.findByName(name);
    }

    @Override
    public boolean delete(Integer id) {
        return repository.delete(id);
    }

    @Override
    public Edition update(Integer id, String name, String description) {
        Edition item = new Edition(id);
        item.setName(name);
        item.setAdditionalText(description);
        return null;
    }
}

package es.gameshelf.domain.services;

import es.gameshelf.domain.Format;
import es.gameshelf.domain.interfaces.repository.IFormatRepository;
import es.gameshelf.domain.interfaces.service.IFormatService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

/**
 * @author Nabil L. A. @nalleon
 */
@Service
public class FormatService implements IFormatService {
    /**
     * Properties
     */
    IFormatRepository repository;

    /**
     * Setter for the autowired service
     * @param repository of the service
     */
    @Autowired
    public void setRepository(IFormatRepository repository) {
        this.repository = repository;
    }

    @Override
    public Format add(String name) {
        Format item = new Format();
        item.setName(name);
        return repository.save(item);
    }

    @Override
    public List<Format> findAll() {
        return repository.findAll();
    }

    @Override
    public Format findById(Integer id) {
        return repository.findById(id);
    }

    @Override
    public Format findByName(String name) {
        return repository.findByName(name);
    }

    @Override
    public boolean delete(Integer id) {
        return repository.delete(id);
    }

    @Override
    public Format update(Integer id, String name) {
        Format item = new Format(id);
        item.setName(name);
        return repository.save(item);    }
}

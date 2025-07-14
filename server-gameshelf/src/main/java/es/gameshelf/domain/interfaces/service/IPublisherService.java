package es.gameshelf.domain.interfaces.service;

import es.gameshelf.domain.Publisher;

import java.util.List;

/**
 * @author Nabil L. A. @nalleon
 */
public interface IPublisherService {
    Publisher add(String name);
    List<Publisher> findAll();
    Publisher findById(Integer id);
    Publisher findByName(String name);
    boolean delete(Integer id);
    Publisher update(Integer id, String name);
}
